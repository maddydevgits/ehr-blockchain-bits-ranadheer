from flask import Flask, render_template, redirect, request, session
from web3 import Web3, HTTPProvider
from time import sleep
import json

def connect_with_blockchain(acc):
    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    if(acc==0):
        web3.eth.defaultAccount = web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=acc
    compiled_contract_path='../build/contracts/ehr.json'

    with open(compiled_contract_path) as file:
        contract_json=json.load(file)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return contract, web3

app=Flask(__name__)
app.secret_key='makeskilled'

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/registerUser',methods=['GET','POST'])
def registerUser():
    username=request.form['username']
    walletaddr=request.form['walletaddr']
    password=int(request.form['password'])
    email=request.form['email']
    role=request.form['role']
    print(username,walletaddr,password,role)
    if(role=='Doctor'):
        print('Registering as Doctor')
        contract,web3=connect_with_blockchain(0)
        tx_hash=contract.functions.addDoctor(email,walletaddr,username,password).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
    elif(role=='Patient'):
        print('Registering as Patient')
        contract,web3=connect_with_blockchain(0)
        tx_hash=contract.functions.addPatient(email,walletaddr,username,password).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('login.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/loginUser',methods=['GET','POST'])
def loginUser():
    walletaddr=request.form['walletaddr']
    password=int(request.form['password'])
    role=''
    contract,web3=connect_with_blockchain(0)
    _demails,_doctors,_dnames,_dpasswords=contract.functions.viewDoctors().call()
    _pemails,_patients,_pnames,_ppasswords=contract.functions.viewPatients().call()

    if walletaddr in _demails:
        role='Doctor'
    elif walletaddr in _pemails:
        role='Patient'
    print(role)
    if role=='Doctor':
        doctorIndex=_demails.index(walletaddr)
        if(_dpasswords[doctorIndex]==password):
            session['walletaddr']=_doctors[doctorIndex]
            return redirect('/ddashboard')
        else:
            return redirect('/login')
    
    if role=='Patient':
        patientIndex=_pemails.index(walletaddr)
        if(_ppasswords[patientIndex]==password):
            session['walletaddr']=_patients[patientIndex]
            return redirect('/pdashboard')
        else:
            return redirect('/login')

@app.route('/ddashboard')
def ddashboard():
    data=[]
    walletaddr=session['walletaddr']
    contract,web3=connect_with_blockchain(0)
    _appids,_cdoctors,_cpatients,_cdates,_cstatus=contract.functions.viewAppointments().call()
    for i in range(len(_cdoctors)):
        if _cdoctors[i]==walletaddr:
            if _cstatus[i]==False:
                dummy=[]
                dummy.append(_appids[i])
                dummy.append(_cpatients[i])
                dummy.append(_cdates[i])
                data.append(dummy)
    l=len(data)
    return render_template('ddashboard.html',dashboard_data=data,len=l)

@app.route('/pdashboard')
def pdashboard():
    data=[]
    contract,web3=connect_with_blockchain(0)
    _demails,_doctors,_dnames,_dpasswords=contract.functions.viewDoctors().call()
    for i in range(len(_doctors)):
        dummy=[]
        dummy.append(_doctors[i])
        dummy.append(_dnames[i])
        data.append(dummy)
    l=len(data)
    return render_template('pdashboard.html',dashboard_data=data,len=l)

@app.route('/bookappointmentform',methods=['GET','POST'])
def bookappointmentform():
    walletaddr=session['walletaddr']
    doctorform=request.form['doctorform']
    date=request.form['date']
    print(doctorform,date)
    contract,web3=connect_with_blockchain(0)
    tx_hash=contract.functions.createAppointment(doctorform,walletaddr,str(date)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/pdoctorcons')

@app.route('/pdoctorcons')
def pdoctorcons():
    data=[]
    walletaddr=session['walletaddr']
    contract,web3=connect_with_blockchain(0)
    _appids,_cdoctors,_cpatients,_cdates,_cstatus=contract.functions.viewAppointments().call()
    _cfullNames,_cdobs,_cgenders,_caddresses,_cphones,_cemails,_cemergNames,_cemergRelations,_cemergContacts=contract.functions.viewDemographics().call()
    _cmeds,_callergies,_cpastMedHistory,_cfamMedHistory,_csocialHistory=contract.functions.viewMedicalHistory().call()
    _cbp,_cpulse,_ctemp,_crespiratoryRate,_cweight,_cheight,_cbmi,_creasonforvisit,_cphysicalexamination,_cdiagnosis=contract.functions.viewClinicalData().call()
    print(_cdoctors,_cpatients,_cdates,_cstatus)
    print(_cfullNames,_cdobs,_cgenders,_caddresses,_cphones,_cemails,_cemergNames,_cemergRelations,_cemergContacts)
    print(_cmeds,_callergies,_cpastMedHistory,_cfamMedHistory,_csocialHistory)
    for i in range(len(_cdoctors)):
        if _cpatients[i]==walletaddr and _cstatus[i]==True:
            dummy=[]
            dummy.append(_cdoctors[i])
            dummy.append(_cdates[i])
            dummy.append(_cstatus[i])
            dummy.append(_cfullNames[i])
            dummy.append(_cdobs[i])
            dummy.append(_cgenders[i])
            dummy.append(_caddresses[i])
            dummy.append(_cphones[i])
            dummy.append(_cemails[i])
            dummy.append(_cemergNames[i])
            dummy.append(_cemergRelations[i])
            dummy.append(_cemergContacts[i])
            dummy.append(_cmeds[i])
            dummy.append(_callergies[i])
            dummy.append(_cpastMedHistory[i])
            dummy.append(_cfamMedHistory[i])
            dummy.append(_csocialHistory[i])
            dummy.append(_cbp[i])
            dummy.append(_cpulse[i])
            dummy.append(_ctemp[i])
            dummy.append(_crespiratoryRate[i])
            dummy.append(_cweight[i])
            dummy.append(_cheight[i])
            dummy.append(_cbmi[i])
            dummy.append(_creasonforvisit[i])
            dummy.append(_cphysicalexamination[i])
            dummy.append(_cdiagnosis[i])

            data.append(dummy)
    
    l=len(data)


    return render_template('pdoctorcons.html',dashboard_data=data,len=l)


@app.route('/logout')
def logoutPage():
    return render_template('index.html')

@app.route('/book/<id>/<id1>')
def consultPatient(id,id1):
    print(id)
    session['pid']=id
    session['appid']=int(id1)
    return redirect('/consultPatient')

@app.route('/consultPatient')
def consultpatient():
    return render_template('consultpatient.html')

@app.route('/consultpatientform',methods=['GET','POST'])
def consultpatientform():
    fullName=request.form['fullName']
    dateOfBirth=request.form['dateOfBirth']
    gender=request.form['gender']
    address=request.form['address']
    phone=request.form['phone']
    email=request.form['email']
    emergName=request.form['emergName']
    emergRelation=request.form['emergRelation']
    emergContact=request.form['emergContact']
    meds=request.form['meds']
    allergies=request.form['allergies']
    pastMedHistory=request.form['pastMedHistory']
    famMedHistory=request.form['famMedHistory']
    socialHistory=request.form['socialHistory']
    bp=request.form['bp']
    pulse=request.form['pulse']
    temp=request.form['temp']
    respiratoryRate=request.form['respiratoryRate']
    weight=request.form['weight']
    height=request.form['height']
    bmi=request.form['bmi']
    reasonforvisit=request.form['reasonforvisit']
    physicalexamination=request.form['physicalexamination']
    diagnosis=request.form['diagnosis']

    doctor=session['walletaddr']
    patient=session['pid']
    contract,web3=connect_with_blockchain(0)
    tx_hash=contract.functions.treatPatient(doctor,patient,int(session['appid'])).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash=contract.functions.storeDemographics(fullName,dateOfBirth,gender,address,phone,email,emergName,emergRelation,emergContact).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash=contract.functions.storeMedicalHistory(meds,allergies,pastMedHistory,famMedHistory,socialHistory).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash=contract.functions.storeClinicalData(bp,pulse,temp,respiratoryRate,weight,height,bmi,reasonforvisit,physicalexamination,diagnosis).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/dmypatients')

@app.route('/dmypatients')
def dmypatients():
    data=[]
    doctor=session['walletaddr']
    contract,web3=connect_with_blockchain(0)
    _appids,_cdoctors,_cpatients,_cdates,_cstatus=contract.functions.viewAppointments().call()
    for i in range(len(_cdoctors)):
        if _cdoctors[i]==doctor:
            dummy=[]
            dummy.append(_cpatients[i])
            dummy.append(_cdates[i])
            dummy.append(_cstatus[i])
            dummy.append(_appids[i])
            data.append(dummy)
    l=len(data)
    return render_template('dmypatients.html',dashboard_data=data,len=l)

@app.route('/viewConsultationsPublic',methods=['post'])
def viewConsultationsPublic():
    walletaddr=request.form['walletaddr']
    password=request.form['password']

    contract,web3=connect_with_blockchain(0)
    _pemails,_patients,_pnames,_ppasswords=contract.functions.viewPatients().call()

    print(_patients,_ppasswords)

    for i in range(len(_patients)):
        if _pemails[i]==walletaddr and _ppasswords[i]==int(password):
            session['walletaddr']=_patients[i]
            return redirect('/viewPublic')
    return render_template('viewconsultations.html',err='You cant access them')

@app.route('/viewconsultations')
def viewconsultations():
    return render_template('viewconsultations.html')

@app.route('/viewPublic')
def viewPublic():
    data=[]
    walletaddr=session['walletaddr']
    contract,web3=connect_with_blockchain(0)
    _appids,_cdoctors,_cpatients,_cdates,_cstatus=contract.functions.viewAppointments().call()
    _cfullNames,_cdobs,_cgenders,_caddresses,_cphones,_cemails,_cemergNames,_cemergRelations,_cemergContacts=contract.functions.viewDemographics().call()
    _cmeds,_callergies,_cpastMedHistory,_cfamMedHistory,_csocialHistory=contract.functions.viewMedicalHistory().call()
    _cbp,_cpulse,_ctemp,_crespiratoryRate,_cweight,_cheight,_cbmi,_creasonforvisit,_cphysicalexamination,_cdiagnosis=contract.functions.viewClinicalData().call()
    for i in range(len(_cdoctors)):
        if _cpatients[i]==walletaddr and _cstatus[i]==True:
            dummy=[]
            dummy.append(_cdoctors[i])
            dummy.append(_cdates[i])
            dummy.append(_cstatus[i])
            dummy.append(_cfullNames[i])
            dummy.append(_cdobs[i])
            dummy.append(_cgenders[i])
            dummy.append(_caddresses[i])
            dummy.append(_cphones[i])
            dummy.append(_cemails[i])
            dummy.append(_cemergNames[i])
            dummy.append(_cemergRelations[i])
            dummy.append(_cemergContacts[i])
            dummy.append(_cmeds[i])
            dummy.append(_callergies[i])
            dummy.append(_cpastMedHistory[i])
            dummy.append(_cfamMedHistory[i])
            dummy.append(_csocialHistory[i])
            dummy.append(_cbp[i])
            dummy.append(_cpulse[i])
            dummy.append(_ctemp[i])
            dummy.append(_crespiratoryRate[i])
            dummy.append(_cweight[i])
            dummy.append(_cheight[i])
            dummy.append(_cbmi[i])
            dummy.append(_creasonforvisit[i])
            dummy.append(_cphysicalexamination[i])
            dummy.append(_cdiagnosis[i])

            data.append(dummy)
    
    l=len(data)

    return render_template('viewpublic.html',dashboard_data=data,len=l)


if __name__=="__main__":
    app.run(debug=True)