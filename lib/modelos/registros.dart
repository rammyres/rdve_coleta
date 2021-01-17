import 'dart:typed_data';
import 'dart:convert';
import 'package:merkletree/merkletree.dart';
import 'package:rdve_coleta/modelos/candidatura.dart';
import 'package:rdve_coleta/modelos/eleitor.dart';
import 'package:rdve_coleta/modelos/mesario.dart';
import 'package:crypto/crypto.dart';

class Registros {
  List<Mesario> operadores = [];
  List<Eleitor> eleitores = [];
  List<Candidato> candidatos = [];
  MerkleTree arvore;

  void adicionar(var elemento) {
    if (elemento is Eleitor) this.eleitores.add(elemento);
    if (elemento is Candidato) this.candidatos.add(elemento);
    if (elemento is Mesario) this.operadores.add(elemento);
  }

  Uint8List hasher(var dados) {
    return sha256.convert(dados.toString().codeUnits).toString().codeUnits;
  }

  MerkleTree montarArvore() {
    List tmp = [];

    tmp.addAll(eleitores);
    tmp.addAll(operadores);
    tmp.addAll(candidatos);

    var folhas =
        tmp.map((f) => sha256.convert(f.id.codeUnits).toString().codeUnits);

    return MerkleTree(leaves: folhas, hashAlgo: hasher);
  }

  String exportarRegistros() {
    List tmp = [];

    tmp.addAll(eleitores);
    tmp.addAll(operadores);
    tmp.addAll(candidatos);

    arvore = montarArvore();

    return json.encode({
      'header': "produto_registro",
      'raiz_merkle': arvore.root.toString(),
      'eleitores': eleitores
          .map((e) => {
                'eleitor': e.nome,
                'id': e.id,
                'endereco': e.endereco,
                'chavePublica': e.chavePublica.toString(),
              })
          .toList(),
      'operadores': operadores
          .map((e) => {
                'operador': e.nome,
                'id_operador': e.id,
                'chavePublica_operador': e.chavePublica.toString(),
              })
          .toList(),
      'candidatos': candidatos
          .map((e) => {
                'candidato': e.apelido,
                'id_candidato': e.id,
                'endereco_candidato': e.endereco,
                'assinatura': e.assinatura,
                'chavePublica_cand': e.chavePublica.toString(),
              })
          .toList(),
      'arvore': arvore.toString(),
    });
  }
}
