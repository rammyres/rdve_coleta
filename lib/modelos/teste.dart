import 'dart:convert';
import 'dart:typed_data';
import 'package:asn1lib/asn1lib.dart';
import 'package:convert/convert.dart';
import 'package:rdve_coleta/modelos/candidatura.dart';
import 'package:rdve_coleta/modelos/eleitor.dart';
import 'package:rdve_coleta/modelos/registros.dart';
import 'package:secp256k1/secp256k1.dart';
import 'package:crypto/crypto.dart';
import 'mesario.dart';

main() {
  Registros registros = Registros();

  var sk1 = PrivateKey.generate();
  var sk2 = PrivateKey.generate();
  var sk3 = PrivateKey.generate();
  var sk4 = PrivateKey.generate();
  var sk5 = PrivateKey.generate();
  var sk6 = PrivateKey.generate();
  var sk7 = PrivateKey.generate();

  Eleitor eleitor1 = Eleitor(
    nome: 'eleitor1',
    id: 'id1',
    endereco: 'endereco1',
    chavePublica: sk1.publicKey.toString(),
  );
  Eleitor eleitor2 = Eleitor(
    nome: 'eleitor2',
    id: 'id2',
    endereco: 'endereco2',
    chavePublica: sk2.publicKey.toString(),
  );
  Eleitor eleitor3 = Eleitor(
    nome: 'eleitor3',
    id: 'id3',
    endereco: 'endereco3',
    chavePublica: sk3.publicKey.toString(),
  );
  Eleitor eleitor4 = Eleitor(
    nome: 'eleitor4',
    id: 'id4',
    endereco: 'endereco4',
    chavePublica: sk4.publicKey.toString(),
  );
  Eleitor eleitor5 = Eleitor(
    nome: 'eleitor5',
    id: 'id5',
    endereco: 'endereco5',
    chavePublica: sk5.publicKey.toString(),
  );
  Eleitor eleitor6 = Eleitor(
    nome: 'eleitor6',
    id: 'id6',
    endereco: 'endereco6',
    chavePublica: sk6.publicKey.toString(),
  );
  Eleitor eleitor7 = Eleitor(
    nome: 'eleitor7',
    id: 'id7',
    endereco: 'endereco7',
    chavePublica: sk7.publicKey.toString(),
  );

  registros.adicionar(eleitor1);
  registros.adicionar(eleitor2);
  registros.adicionar(eleitor3);
  registros.adicionar(eleitor4);
  registros.adicionar(eleitor5);
  registros.adicionar(eleitor6);
  registros.adicionar(eleitor7);

  Mesario mesario1 = Mesario(
    nome: 'mesario1',
    id: 'm_id1',
    chavePublica: sk1.publicKey.toString(),
  );
  Mesario mesario2 = Mesario(
    nome: 'mesario2',
    id: 'm_id2',
    chavePublica: sk2.publicKey.toString(),
  );
  Candidato candidato1 = Candidato(
    apelido: 'apelido1',
    id: 'cand_id1',
    endereco: 'end_cand1',
    chavePublica: sk3.publicKey.toString(),
    timestamp: DateTime.now().millisecondsSinceEpoch.toString(),
    assinatura: sha256.convert('apelido1'.codeUnits).toString(),
  );
  Candidato candidato2 = Candidato(
    apelido: 'apelido2',
    id: 'cand_id2',
    endereco: 'end_cand2',
    chavePublica: sk4.publicKey.toString(),
    timestamp: DateTime.now().millisecondsSinceEpoch.toString(),
    assinatura: sha256.convert('apelido2'.codeUnits).toString(),
  );

  registros.adicionar(mesario1);
  registros.adicionar(mesario2);
  registros.adicionar(candidato1);
  registros.adicionar(candidato2);

  print(registros.exportarRegistros());

  var teste = json.decode(registros.exportarRegistros());
  print(teste['candidatos'][1]);
}
