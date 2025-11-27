from sqlmodel import select
from sqlalchemy.orm import selectinload
from ..db.db import AsyncSession
from ..models.DoctorModel import Doctor
from ..schemas.DoctorSchemas import DoctorCreate,DoctorUpdate
from ..schemas.common import LatestSymptoms
from ..schemas.PatientSchemas import PatientUpdateStatus
from ..models.PatientModel import Patient
from ..schemas.types import Binary,Seizures,FinalStateEnum,Four_Classes


class DoctorServices:
    
    def update(self,doctor:Doctor,doctor_data:DoctorUpdate,session:AsyncSession):
        for k,v in doctor_data.model_dump(exclude_unset=True).items():
            setattr(doctor, k, v)
        session.add(doctor)
        return doctor
    
        
    async def get(self,doctor_id:str,session:AsyncSession)->Doctor:
        doctor = await session.get(Doctor, doctor_id)
        return doctor 
    
    
        
    
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=100):
        statement = select(Doctor).offset((page-1)*limit).limit(limit)
        result = await session.exec(statement)
        return result.all() 
    
    
    def add( self,doctor_data:DoctorCreate,session:AsyncSession):
        doctor =Doctor(**(doctor_data.model_dump()))
        session.add(doctor)
        return doctor 
    
    async def get_by_user_id(self,user_id:str,session:AsyncSession):
        statement = select(Doctor).where(Doctor.user_id == user_id)
        doctor = (await session.exec(statement)).first()
        return doctor
    
    async def detete(self,doctor:Doctor,session:AsyncSession):
        result = await session.exec(select(Patient).where(Patient.doctor_id == doctor.id))
        patients = result.all()
        for patient in patients:
            patient.doctor_id = None  
            session.add(patient)
        await session.delete(doctor)
        
    
    def to_check(self, patient: Patient, latest_symptoms: LatestSymptoms):
        if latest_symptoms.general_symptoms is None and \
        latest_symptoms.specific_symtoms is None and \
        latest_symptoms.radio_image is None:
            return None

        rd = latest_symptoms.radio_image
        gs = latest_symptoms.general_symptoms
        ss = latest_symptoms.specific_symtoms

        # RULE 1
        if patient.age > 62 and patient.antecedents > 0 and gs and gs.seizures == 2 and gs.drowsiness == 1 and rd and rd.type >= 2:
            return {
                "rule_id": 1,
                "rule_description": (
                    "Patient older than 62 years with medical antecedents, "
                    "showing moderate seizures and mild drowsiness combined "
                    "with a high-grade abnormality on radiological imaging. "
                    "This pattern indicates a high probability of a malignant brain tumor "
                    "requiring urgent medical intervention and hospitalization."
                ),
                "result": PatientUpdateStatus(
                    tumor_status=Binary.ONE,
                    hospitalisation=Four_Classes.TWO,
                    final_state=FinalStateEnum.T
                )
            }

        # RULE 2
        if ss and gs and ss.pressure >= 2 and gs.fatigue == 2 and gs.memory_pb >= 2:
            return {
                "rule_id": 2,
                "rule_description": (
                    "Patient presents increased intracranial pressure symptoms, "
                    "severe fatigue and significant memory impairment. "
                    "This clinical combination strongly suggests neurological dysfunction "
                    "associated with a progressing brain tumor, requiring diagnostic confirmation."
                ),
                "result": PatientUpdateStatus(
                    tumor_status=Binary.ONE,
                    hospitalisation=Four_Classes.ONE,
                    final_state=FinalStateEnum.D
                )
            }

        # RULE 3
        if ss and gs and ss.balance_loss == 1 and ss.muscle >= 2 and patient.age > 50:
            return {
                "rule_id": 3,
                "rule_description": (
                    "Patient over 50 years old experiencing loss of balance with muscle weakness. "
                    "These symptoms indicate potential neurological motor disruption, "
                    "often linked to tumors affecting the cerebellum or motor cortex regions."
                ),
                "result": PatientUpdateStatus(
                    tumor_status=Binary.ONE,
                    hospitalisation=Four_Classes.TWO,
                    final_state=FinalStateEnum.T
                )
            }

        # RULE 4
        if ss and gs and ss.judgment_degradation >= 2 and ss.sense_degradation >= 2 and gs.seizures == Seizures.TC:
            return {
                "rule_id": 4,
                "rule_description": (
                    "Patient demonstrates cognitive degradation with altered judgment, "
                    "sensory impairment and tonic-clonic seizures. "
                    "This neurological profile indicates a severe cerebral disorder, "
                    "strongly linked to malignant brain tumor progression."
                ),
                "result": PatientUpdateStatus(
                tumor_status=Binary.ONE,
                hospitalisation=Four_Classes.TWO,
                final_state=FinalStateEnum.T
            )
        }

        # RULE 5
        if gs and rd and gs.seizures == Seizures.M and gs.fatigue <= 1 and rd.type == 0:
            return {
                "rule_id": 5,
                "rule_description": (
                    "Patient shows mild seizure activity, low fatigue level and no abnormal findings "
                    "on radiological imaging. This indicates a low probability of brain tumor "
                    "and suggests normal neurological condition."
                ),
                "result": PatientUpdateStatus(
                    tumor_status=Binary.ZERO,
                    hospitalisation=Four_Classes.ZERO,
                    final_state=FinalStateEnum.N
                )
            }

        # RULE 6
        if gs and gs.drowsiness == 2 and ss and ss.pressure >= 2 and patient.age > 55:
            return {
                "rule_id": 6,
                "rule_description": (
                    "Patient older than 55 with severe drowsiness and high intracranial pressure symptoms. "
                    "This pattern is often associated with tumors causing increased brain compression "
                    "and requires immediate neurological evaluation."
                ),
                "result": PatientUpdateStatus(
                    tumor_status=Binary.ONE,
                    hospitalisation=Four_Classes.TWO,
                    final_state=FinalStateEnum.T
                )
            }

        # RULE 7
        if gs and gs.fatigue == 2 and gs.memory_pb >= 1 and gs.seizures in [Seizures.TC, Seizures.S]:
            return {
                "rule_id": 7,
                "rule_description": (
                    "Patient suffering from severe fatigue, memory problems and recurrent seizures. "
                    "This triad of symptoms is a strong indicator of a possible intracranial tumor "
                    "affecting both cognitive and neurological pathways."
                ),
                "result": PatientUpdateStatus(
                    tumor_status=Binary.ONE,
                    hospitalisation=Four_Classes.ONE,
                    final_state=FinalStateEnum.D
                )
            }

        # RULE 8
        if gs and ss and ss.muscle >= 2 and ss.swallowing >= 2 and rd and rd.type >= 2:
            return {
                "rule_id": 8,
                "rule_description": (
                    "Patient shows difficulty in muscle control and swallowing associated "
                    "with severe abnormalities in radiological imaging. "
                    "This indicates advanced neurological impairment caused by tumor progression "
                    "in critical brainstem regions."
                ),
                "result": PatientUpdateStatus(
                    tumor_status=Binary.ONE,
                    hospitalisation=Four_Classes.THREE,
                    final_state=FinalStateEnum.R
                )
            }

        # No rule matched
        return {
            "rule_id": None,
            "rule_description": "No predefined clinical rule matched the patient symptoms.",
            "result": None
        }





