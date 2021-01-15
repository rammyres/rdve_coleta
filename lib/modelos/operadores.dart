import 'dart:convert';

import 'mesario.dart';

class Operadores {
  List<Mesario> mesarios = [];

  Operadores({List<Mesario> mesarios}) {
    if (mesarios != null) {
      this.mesarios.addAll(mesarios);
    }
  }

  void adicionarMesario(Mesario mesario) {
    this.mesarios.add(mesario);
  }

  int procurarMesario({
    String nome,
    String id,
  }) {
    if (nome != null) {
      for (var op in this.mesarios) {
        if (op.nome == nome) return mesarios.indexOf(op);
      }
    }

    if (id != null) {
      for (var op in this.mesarios) {
        if (op.id == id) return mesarios.indexOf(op);
      }
    }

    return null;
  }

  String paraJson() {
    return json.encode(
      {
        'header': 'operadores',
        'mesarios': this
            .mesarios
            .map(
              (e) => {
                'id': e.id,
                'nome': e.nome,
                'chavePublica': e.chavePublica.toString(),
              },
            )
            .toString(),
      },
    );
  }
}
