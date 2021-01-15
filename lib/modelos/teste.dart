import 'package:secp256k1/secp256k1.dart';

import 'mesario.dart';
import 'operadores.dart';

main() {
  Operadores op = new Operadores();

  var sk1 = PrivateKey.generate();
  var sk2 = PrivateKey.generate();
  var sk3 = PrivateKey.generate();

  Mesario mesario1 = Mesario(
    id: 'id1',
    nome: 'nome1',
    chavePublica: sk1.publicKey.toString(),
  );
  Mesario mesario2 = Mesario(
    id: 'id2',
    nome: 'nome2',
    chavePublica: sk2.publicKey.toString(),
  );
  Mesario mesario3 = Mesario(
    id: 'id3',
    nome: 'nome3',
    chavePublica: sk3.publicKey.toString(),
  );

  op.adicionarMesario(mesario1);
  op.adicionarMesario(mesario2);
  op.adicionarMesario(mesario3);

  print(op.paraJson());

  print(op.procurarMesario(nome: 'nome2'));
}
