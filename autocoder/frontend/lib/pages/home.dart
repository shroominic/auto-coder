import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  HomePageState createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  bool _useAccessToken = false;
  String _issueUrl = '';
  String? _accessToken;

  Future<void> createIssue() async {
    const String apiUrl = 'http://127.0.0.1:8000/api/issue/create';

    final Map<String, String> headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json',
    };

    final Map<String, String> body = {
      'issue_url': _issueUrl,
      'access_token': _accessToken ?? '',
    };

    final response = await http.post(
      Uri.parse(apiUrl),
      headers: headers,
      body: jsonEncode(body),
    );

    if (response.statusCode == 200) {
      print('Issue created successfully');
    } else {
      print('Failed to create issue. Status code: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AutoCodr'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              constraints: const BoxConstraints(maxWidth: 420),
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: TextField(
                onChanged: (String value) {
                  setState(() {
                    _issueUrl = value;
                  });
                },
                decoration: const InputDecoration(
                  labelText: 'github issue link',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            if (_useAccessToken)
              Container(
                constraints: const BoxConstraints(maxWidth: 420),
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: TextField(
                  onChanged: (String value) {
                    setState(() {
                      _accessToken = value;
                    });
                  },
                  decoration: const InputDecoration(
                    labelText: 'access token',
                    border: OutlineInputBorder(),
                  ),
                ),
              ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                createIssue();
              },
              child: const Text('Solve it!'),
            ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Checkbox(
                  value: _useAccessToken,
                  onChanged: (bool? value) {
                    setState(() {
                      _useAccessToken = value!;
                    });
                  },
                ),
                const Text('Use access token for private repos'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
