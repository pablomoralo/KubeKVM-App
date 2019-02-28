import requests
import sys, subprocess
import libvirt
import time
#import json

#COSAS NECESARIAS PARA HACER EL GET DE LOS DATOS
#-----------------------------------------------
def getDeployments(url, deploymentsDictionary):
    #url = 'http://localhost:3000/api/deployments'
    response = requests.get(url)
    print('DICCIONARIO EN GET')
    print('------------------')
    print deploymentsDictionary
    #diccionario={}
    #print(response.content)
    if response.status_code==200:
        payload=response.json()
        deployments=payload.get('deployments',[])
        if deployments:#Si no esta vacia
            for deployment in deployments:
                print(deployment)
                #name=deployment['name']
                #print(name)
                if deployment['estado']=='Pendiente':
                    deploymentsDictionary[deployment['_id']]=[]
                    #newUrl=url+'/'+deployment['_id']
                    #print(url+'/'+deployment['_id'])
                    #print(newUrl)
                    updateDeployment('http://localhost:3000/deployments/editDeployment/'+deployment['_id'], 'Activo')
                    deploymentsDictionary[deployment['_id']]=kvmDeployment(deployment['type'], deployment['replicas'], deployment['name'])
                    startDeploymentMachines(deploymentsDictionary[deployment['_id']])
                elif deployment['estado']=='Activo':
                    for i in range(len(deploymentsDictionary)):
                        if deploymentsDictionary.keys()[i]==deployment['_id']:#diccionario.keys devuelve una tupla con id y nombresMaquinas
                            checkState('http://localhost:3000/deployments/editDeployment/', deploymentsDictionary.items()[i])
    return deploymentsDictionary

def checkState(url, deployment):
    print('DICCIONARIO EN VIEW')
    print('------------------')
    print deployment
    i=0
    print deployment[1]
    for name in deployment[1]:
        for dom in conn.listAllDomains():
            if name in dom.name():
                #if name==dom.name():
                print(name+'=='+dom.name())
                if dom.state()[0]==5:
                    print('MAQUINA APAGADA')
                    i+=1
                    if i==len(deployment[1]):
                        print('Pasando despliegue '+deployment[0]+' a estado Inactivo...')
                        updateDeployment(url+deployment[0], 'Inactivo')

def startDeploymentMachines(deploymentsMachines):
    print deploymentsMachines
    for name in deploymentsMachines:
        print('Iniciando maquina '+name)
        command = 'sudo virsh start '+name
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        for output in result.stdout:
            print(output.decode(sys.getdefaultencoding()).rstrip())

#COSAS NECESARIAS PARA HACER EL UPDATE DE LOS DATOS
#-----------------------------------------------
def updateDeployment(url, state):
    #url='http://localhost:3000/api/deployments/5be48a73807a4719bbb7d579'
    payload={'estado':state}
    response=requests.put(url, data=payload)

    if response.status_code==200:
        print('Despliegue actualizado satisfactoriamente al estado '+state)

#COSAS NECESARIAS PARA HACER EL DELETE DE LOS DATOS
#-----------------------------------------------
def deleteDeployment(url):
    #url='http://localhost:3000/api/deployments/5be48d4436e9d81d2c76bff9'
    response=requests.delete(url)

    if response.status_code==200:
        print(response.content)

def kvmDeployment(type, replicas, name):
    machineNames=[]
    for i in range(replicas):
        if type=='TecnologiaDeComputadores':
            print('Desplegando maquina de Tecnologia de Computadores '+'winxp-'+name+'-'+str(i+1))
            #print('winxp'+'-deployment'+str(i+1))
            machineNames.append('winxp-'+name+'-'+str(i+1))
            command = 'sudo virt-clone --connect qemu:///system --original winxp --name winxp-'+name+'-'+str(i+1)+' --file /var/lib/libvirt/images/winxp-'+name+'-'+str(i+1)+'.qcow2'
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            for output in result.stdout:
                print(output.decode(sys.getdefaultencoding()).rstrip())
            #sudo virt-clone --connect qemu:///system --original winxp --name winxp_clone2 --file /var/lib/libvirt/images/winxp_clone2.qcow2
        elif type=='RedesNeuronales':
            print('Desplegando maquina de Redes Neuronales '+'ubuntu16.04-'+name+'-'+str(i+1))
            #print('ubuntu16.04'+'-deployment'+str(i+1))
            machineNames.append('ubuntu16.04-'+name+'-'+str(i+1))
            command = 'sudo virt-clone --connect qemu:///system --original ubuntu16.04 --name ubuntu16.04-'+name+'-'+str(i+1)+' --file /var/lib/libvirt/images/ubuntu16.04-'+name+'-'+str(i+1)+'.qcow2'
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            for output in result.stdout:
                print(output.decode(sys.getdefaultencoding()).rstrip())
            #sudo virt-clone --connect qemu:///system --original winxp --name winxp_clone2 --file /var/lib/libvirt/images/winxp_clone2.qcow2
    return machineNames

if __name__ == '__main__':

    url='http://localhost:3000/deploymentsScript'
    conn=libvirt.open("qemu:///system")
    deploymentsDictionary={}
    """deploymentsDictionary=getDeployments(url, deploymentsDictionary)
    print('DICCIONARIO')
    print('-----------')
    print deploymentsDictionary

    deploymentsDictionary=getDeployments(url, deploymentsDictionary)
    """
    while True:
        print('==============================================================================')
        deploymentsDictionary=getDeployments(url, deploymentsDictionary)
        time.sleep(30)
        print('==============================================================================')

    """
    print('DICCIONARIO')
    print('-----------')
    print deploymentsDictionary.items()[i]
    print deploymentsDictionary
    for dic in deploymentsDictionary:
        for machine in deploymentsDictionary[dic]:
            print machine
        print dic
        print deploymentsDictionary[dic]
        print len(deploymentsDictionary[dic])"""''
