const express = require('express');
const router = express.Router();

const Deployment = require('../models/deployment');

router.get('/deployments/add', (req, res) => {
  res.render('deployments/newDeployment');
});

router.post('/deployments/newDeployment', (req, res) => {
  //const name , type, replicas = req.body;
  const name = req.body.name;
  const type = req.body.type;
  const replicas = req.body.replicas;
  const errors= [];
  if(!name){
    errors.push({text: 'Por favor escribe un nombre para el despliegue'});
  }
  if(errors.length > 0) {
    res.render('deployments/newDeployment', {
      errors,
      name,
      type,
      replicas
    });
  }else{
    const newDeployment = new Deployment({name, type, replicas});
    newDeployment.save();
    req.flash('success_msg', 'Despliegue Creado Satisfactoriamente');
    res.redirect('/deployments');
  }
});

router.get('/deployments', (req, res) => {
  Deployment.find({}, (err, deployments) =>{
    if (err) return res.status(500).send({message: `Error al realizar la peticion: ${err}`});
    if(!deployments) return res.status(404).send({message: 'No existen despliegues'});

    //res.status(200).send({deployments: deployments});
    res.render('deployments/allDeployments', {deployments});
  });
});

router.get('/deploymentsScript', (req, res) => {
  Deployment.find({}, (err, deployments) =>{
    if (err) return res.status(500).send({message: `Error al realizar la peticion: ${err}`});
    if(!deployments) return res.status(404).send({message: 'No existen despliegues'});

    res.status(200).send({deployments: deployments});
  });
});

router.get('/deployments/edit/:id', (req, res) => {
  /*const deployment = Deployment.findById(req.params.id);
  res.render('deployments/editDeployment', {deployment});
  */
  Deployment.findById(req.params.id, (err, deployment) => {
    if (err) return res.status(500).send({message: `Error al realizar la peticion: ${err}`});
    if(!deployment) return res.status(404).send({message: 'El despliegue no existe'});

    res.render('deployments/editDeployment', {deployment});
  });
});

router.put('/deployments/editDeployment/:id', (req, res) => {
  Deployment.findByIdAndUpdate(req.params.id, req.body, (err, deploymentUpdated) => {
    if (err) return res.status(500).send({message: `Error al actualizar el despliegue: ${err}`});
    if(!deploymentUpdated) return res.status(404).send({message: 'El despliegue no existe'});
    req.flash('success_msg', 'Despliegue Actualizado Satisfactoriamente');
    res.redirect('/deployments');
  });
});

router.delete('/deployments/delete/:id', (req, res) => {

  Deployment.findById(req.params.id, (err, deployment) => {
    if (err) return res.status(500).send({message: `Error al borrar el despliegue: ${err}`});
    if(!deployment) return res.status(404).send({message: 'El despliegue no existe'});
    deployment.remove(err => {
      if (err) return res.status(500).send({message: `Error al borrar el despliegue: ${err}`});
      req.flash('success_msg', 'Despliegue Eliminado Satisfactoriamente');
      res.redirect('/deployments');
    })
  })
})

module.exports = router;
