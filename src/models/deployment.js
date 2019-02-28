const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const DeploymentSchema = Schema({
  name: { type:String, unique:true, required:true},
  /*Si llega un tipo que no es TC o RN no se va a almacenar*/
  type: { type: String, enum: ['TecnologiaDeComputadores', 'RedesNeuronales'] },
  replicas: { type: Number, default: 1 },
  estado: { type: String, enum: ['Inactivo', 'Pendiente', 'Activo'], default: 'Pendiente'}
})

module.exports = mongoose.model('Deployment', DeploymentSchema);
