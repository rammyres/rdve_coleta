import 'dart:convert';
import 'package:secp256k1/secp256k1.dart';

class Candidato {
  String id;
  String numero;
  String apelido;
  String endereco;
  String timestamp;
  String assinatura;
  PublicKey chavePublica;

  Candidato({
    this.id,
    this.apelido,
    this.numero,
    this.endereco,
    this.timestamp,
    this.assinatura,
    chavePublica,
  }) {
    this.chavePublica = PublicKey.fromHex(chavePublica);
  }

  String paraJson() {
    return json.encode({
      'header': 'candidatura',
      'id': this.id,
      'apelido': this.apelido,
      'numero': this.numero,
      'endereco': this.endereco,
      'assinatura': this.assinatura,
      'chavePublica_cand': this.chavePublica.toHex(),
    });
  }
}
