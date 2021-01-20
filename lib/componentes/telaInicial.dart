import 'package:qrscan/qrscan.dart' as scanner;
import 'package:flutter/material.dart';

class TelaInicial extends StatefulWidget {
  @override
  _TelaInicialState createState() => _TelaInicialState();
}

class _TelaInicialState extends State<TelaInicial> {
  String resultado;

  void lerQr() async {
    var result = await scanner.scan();
    print(result);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Solicitar registro de eleitores, mesários e candidatos',
          style: TextStyle(
            fontSize: 28,
            color: Colors.white,
          ),
        ),
      ),
      body: Container(
        child: Column(
          children: [
            Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                ButtonTheme(
                  minWidth: 300,
                  child: RaisedButton(
                    color: Colors.green,
                    onPressed: () => lerQr(),
                    child: Column(
                      children: [
                        Icon(
                          Icons.account_box_rounded,
                          color: Colors.white,
                          size: 180,
                        ),
                        Text(
                          "Cadastrar eleitor",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 28,
                            color: Colors.white,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                ButtonTheme(
                  minWidth: 300,
                  child: RaisedButton(
                      color: Colors.red,
                      child: Column(
                        children: [
                          Icon(
                            Icons.account_box_rounded,
                            size: 180,
                            color: Colors.white,
                          ),
                          Text(
                            "Registrar candidatura",
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 28,
                              color: Colors.white,
                            ),
                          ),
                        ],
                      ),
                      onPressed: () {}),
                ),
              ],
            ),
            Spacer(),
          ],
        ),
      ),
    );
  }
}
