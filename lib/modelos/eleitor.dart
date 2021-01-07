import 'dart:convert';

import 'package:secp256k1/secp256k1.dart';

class Eleitor {
  String id;
  String nome;
  String endereco;
  PublicKey chavePublica;

  Eleitor({
    this.id,
    this.nome,
    this.endereco,
    chavePublica,
  }) {
    this.chavePublica = PublicKey.fromHex(chavePublica);
  }

  String paraJson() {
    return json.encode({
      "id": this.id,
      "nome": this.nome,
      "endereco": this.endereco,
      "chavePublica": this.chavePublica.toHex()
    });
  }
}
