import 'dart:convert';

import 'package:autocodr/controller/auth.dart';
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
  String? _githubAccessToken;
  final authController = AuthController();
  bool showLogin = false;
  String login_email = '';
  String login_token = '';
  bool showToken = false;

  Future<void> createIssue() async {
    const String apiUrl = 'http://127.0.0.1:8000/api/issue/solve';
    String _loginAccessToken = 'error';

    if (await authController.isAuthenticated()) {
      _loginAccessToken = authController.user!.accessToken;
    }

    final Map<String, String> headers = {
      'Authorization': 'Bearer $_loginAccessToken',
      'accept': 'application/json',
      'Content-Type': 'application/json',
    };

    final Map<String, String> body = {
      'issue_url': _issueUrl,
      'access_token': _githubAccessToken ?? '',
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
        title: const Text('🤖 AutoCodr'),
        actions: [
          FutureBuilder(
            future: authController.isAuthenticated(),
            builder: (BuildContext context, AsyncSnapshot<bool> snapshot) {
              if (snapshot.hasData) {
                if (snapshot.data!) {
                  return TextButton(
                    onPressed: () {
                      authController.logout();
                    },
                    child: const Text('Logout'),
                  );
                } else {
                  return TextButton(
                    onPressed: () {
                      setState(() {
                        showLogin = !showLogin;
                      });
                    },
                    child: const Text('Login'),
                  );
                }
              } else {
                return const SizedBox();
              }
            },
          )
        ],
      ),
      body: Stack(
        children: [
          Center(
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
                          _githubAccessToken = value;
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
          if (showLogin)
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  if (!showToken)
                    TextField(
                      controller: TextEditingController(text: login_email),
                      onChanged: (value) {
                        login_email = value;
                      },
                      decoration: const InputDecoration(
                        labelText: 'input email',
                        border: OutlineInputBorder(),
                      ),
                    ),
                  if (!showToken)
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: ElevatedButton(
                        onPressed: () {
                          authController.requestEmailLink(login_email);
                          setState(() {
                            showToken = true;
                          });
                        },
                        child: const Text('Send email link'),
                      ),
                    ),
                  if (showToken)
                    TextField(
                      controller: TextEditingController(text: login_token),
                      onChanged: (value) {
                        login_token = value;
                      },
                      decoration: const InputDecoration(
                        labelText: 'input token from email',
                        border: OutlineInputBorder(),
                      ),
                    ),
                  if (showToken)
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: ElevatedButton(
                        onPressed: () {
                          authController.login(login_token);
                        },
                        child: const Text('Login with Token'),
                      ),
                    ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
