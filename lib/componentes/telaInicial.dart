import 'package:flutter/material.dart';

class TelaInicial extends StatelessWidget {
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
                    onPressed: () {},
                    child: Column(
                      children: [
                        Icon(
                          Icons.account_box_rounded,
                          color: Colors.white,
                          size: 190,
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
                  height: 50,
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
