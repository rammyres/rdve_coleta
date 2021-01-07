import 'dart:convert';

import 'package:asn1lib/asn1lib.dart';
import 'package:secp256k1/secp256k1.dart';

class Candidato {
  String id;
  String numero;
  String apelido;
  String endereco;
  String timestamp;
  PublicKey chavePublica;
  Signature assinatura;

  Candidato(
      {this.id,
      this.apelido,
      this.numero,
      this.endereco,
      this.timestamp,
      chavePublica,
      assinatura}) {
        var parser = ASN1Parser(assinatura);
    this.chavePublica = PublicKey.fromHex(chavePublica);
    this.assinatura = ;
      }

  String paraJson() {
    return json.encode({
      'id': this.id,
      'apelido': this.apelido,
      'numero': this.numero,
      'endereco': this.endereco,
      'chavePublica_cand': this.chavePublica.toHex(),
    });
  }
}
