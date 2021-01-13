import 'dart:convert';

import 'package:secp256k1/secp256k1.dart';

class Mesario {
  String id;
  String nome;
  PublicKey chavePublica;

  Mesario({
    this.id,
    this.nome,
    chavePublica,
  }) {
    this.chavePublica = PublicKey.fromHex(chavePublica);
  }

  String paraJson() {
    return json.encode({
      'header': 'mesario',
      'id': this.id,
      'nome': this.nome,
      'chavePublica': this.chavePublica.toString(),
    });
  }
}
