// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

contract ehr {
  
  address[] _doctors;
  string[] _dnames;
  uint[] _dpasswords;
  string[] _demails;

  address[] _patients;
  string[] _pnames;
  uint[] _ppasswords;
  string[] _pemails;

  address[] _cpatients;
  address[] _cdoctors;
  uint[] _appointmentids;

  uint appid=0;
  
  string[] _cfullNames;
  string[] _cdobs;
  string[] _cgenders;
  string[] _caddresses;
  string[] _cphones;
  string[] _cemails;
  string[] _cemergNames;
  string[] _cemergRelations;
  string[] _cemergContacts;

  string[] _cmeds;
  string[] _callergies;
  string[] _cpastMedHistory;
  string[] _cfamMedHistory;
  string[] _csocialHistory;

  string[] _cbp;
  string[] _cpulse;
  string[] _ctemp;
  string[] _crespiratoryRate;
  string[] _cweight;
  string[] _cheight;
  string[] _cbmi;
  string[] _creasonforvisit;
  string[] _cphysicalexamination;
  string[] _cdiagnosis;

  string[] _cdates;
  bool[] _cstatus;

  function addDoctor(string memory email,address doctor, string memory name, uint password) public {
    _doctors.push(doctor);
    _dnames.push(name);
    _demails.push(email);
    _dpasswords.push(password);
  }

  function viewDoctors() public view returns(string[] memory,address[] memory, string[] memory, uint[] memory) {
    return(_demails,_doctors,_dnames,_dpasswords);
  }

  function addPatient(string memory email,address patient, string memory name, uint password) public {
    _patients.push(patient);
    _pnames.push(name);
    _ppasswords.push(password);
    _pemails.push(email);
  }

  function viewPatients() public view returns(string[] memory,address[] memory, string[] memory, uint[] memory){
    return(_pemails,_patients,_pnames,_ppasswords);
  }

  function createAppointment(address doctor, address patient, string memory date) public {
    appid+=1;
    _appointmentids.push(appid);
    _cdoctors.push(doctor);
    _cpatients.push(patient);
    _cdates.push(date);
    _cstatus.push(false);
  }

  function treatPatient(address doctor,address patient,uint aid) public{

    uint i;
    for(i=0;i<_cdoctors.length;i++) {
      if(_cdoctors[i]==doctor && _cpatients[i]==patient && _appointmentids[i]==aid) {
        _cstatus[i]=true;
      }
    }
  }

  function viewAppointments() public view returns(uint[] memory,address[] memory, address[] memory,string[] memory,bool[] memory) {
    return (_appointmentids,_cdoctors,_cpatients,_cdates,_cstatus);
  }

  function storeDemographics(string memory fullName,string memory dob,string memory gender,string memory address1,string memory phone,string memory email,string memory emergName,string memory emergRelation,string memory emergContact) public {
    _cfullNames.push(fullName);
    _cdobs.push(dob);
    _cgenders.push(gender);
    _caddresses.push(address1);
    _cphones.push(phone);
    _cemails.push(email);
    _cemergNames.push(emergName);
    _cemergRelations.push(emergRelation);
    _cemergContacts.push(emergContact);
  }

  function viewDemographics() public view returns(string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory) {
    return(_cfullNames,_cdobs,_cgenders,_caddresses,_cphones,_cemails,_cemergNames,_cemergRelations,_cemergContacts);
  }

  function storeMedicalHistory(string memory meds,string memory allergies,string memory pastMedHistory,string memory famMedHistory,string memory socialHistory) public {
    _cmeds.push(meds);
    _callergies.push(allergies);
    _cpastMedHistory.push(pastMedHistory);
    _cfamMedHistory.push(famMedHistory);
    _csocialHistory.push(socialHistory);
  }

  function viewMedicalHistory() public view returns(string[] memory, string[] memory, string[] memory,string[] memory,string[] memory) {
    return (_cmeds,_callergies,_cpastMedHistory,_cfamMedHistory,_csocialHistory);
  }

  function storeClinicalData(string memory bp,string memory pulse,string memory temp,string memory respiratoryRate,string memory weight,string memory height,string memory bmi,string memory reasonforvisit,string memory physicalexamination,string memory diagnosis) public {
    _cbp.push(bp);
    _cpulse.push(pulse);
    _ctemp.push(temp);
    _crespiratoryRate.push(respiratoryRate);
    _cweight.push(weight);
    _cheight.push(height);
    _cbmi.push(bmi);
    _creasonforvisit.push(reasonforvisit);
    _cphysicalexamination.push(physicalexamination);
    _cdiagnosis.push(diagnosis);
  }

  function viewClinicalData() public view returns(string[] memory, string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory) {
    return(_cbp,_cpulse,_ctemp,_crespiratoryRate,_cweight,_cheight,_cbmi,_creasonforvisit,_cphysicalexamination,_cdiagnosis);
  }

}
