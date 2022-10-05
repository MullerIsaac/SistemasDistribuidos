const express = require('express');
const fs = require('fs');
const router = express.Router();
const net = require('net');
const pb = require('protocol-buffers');
var mensagens = pb(fs.readFileSync('js/message.proto'));

var dispositivos = [];

router.get('/',function(req,res){

      res.render('index',{});
      return;

});


router.get('/descobrir',function(req,res){

  var timeout = 3000;

  var conn = net.createConnection({ port : 9999, host: '127.0.0.1'},() => {

    msg = mensagens.GatewayClient.encode({ tipo : mensagens.GatewayClient.Tipo.DESCOBERTA });

    conn.write(msg);

    return;

  });

  conn.setTimeout(timeout,function(){

    res.render('index',{testemsg: 'Timeout atingido',type : 'warning'});
    conn.end();
    return;

  });

  conn.on('data',function(data){

      msg = new mensagens.GatewayClient.decode(data)

      dispositivos = msg.dispositivos

      var itens = msg.dispositivos

      if(itens.length == 0){

        res.render('index',{testemsg : "Não há dispositivos conectados no momento", itens : itens, type: "info"});
        conn.end();
        return;

      }else{

        res.render('index',{itens : itens});
        conn.end();
        return;

      }

  });

  conn.on('error',function(err){
      res.render('index',{testemsg : 'Falha na conexão', type: 'danger'});
      conn.end();
      return;
  });

});

router.get('/ver/:id',function(req,res){

  var disp = [];

  for( i = 0; i < dispositivos.length ; i++ ){

    if(dispositivos[i].id == req.params.id){

      disp = dispositivos[i];

      break;

    }

  }

  res.render('index',{dispositivo: disp});
  return;

});

router.get('/ausente',function(req,res){

  res.render('index',{testemsg : 'O dispositivo não se encontra na rede', type: 'warning'});
  return;

});

router.post('/executar',function(req,res){

  string = req.body.op.split('-')

  var op = string[1];
  var id = string[0];

  var timeout = 3000;

  var conn = net.createConnection({ port : 9999, host: '127.0.0.1'},() => {

    msg = mensagens.GatewayClient.encode({
      tipo : mensagens.GatewayClient.Tipo.OPERACAO,
      id_dispositivo : id,
      operacao : op
    });

    conn.write(msg);

  });

  conn.setTimeout(timeout,function(){

    res.redirect('/ausente');
    conn.end();

  });


  conn.on('data',function(data){

      var msg = new mensagens.GatewayClient.decode(data);

      var id = msg.id_dispositivo;

      var resposta = msg.resposta;

      var op = msg.operacao;

      var disp = [];

      for( i = 0; i < dispositivos.length; i++){

          if(dispositivos[i].id == id){

            disp = dispositivos[i];

            break;

          }

      }

      res.render('index',{dispositivo: disp, resultado: resposta});

      conn.end();
  });

});

module.exports = router;
