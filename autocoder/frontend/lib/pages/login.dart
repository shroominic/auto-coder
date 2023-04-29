import 'package:autocodr/controller/auth.dart';
import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final authController = AuthController();
  String? email;
  String? token;

  void init() {
    super.initState();
    authController.authStateChanges.listen((authState) {
      if (authState) {
        Navigator.of(context).pushNamedAndRemoveUntil('/', (route) => false);
      }
    });
  }

  void sendEmailLink(String? email) async {
    if (email != null && email.isNotEmpty && email.contains('@')) {
      await authController.requestEmailLink(email);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please enter a valid email address'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.all(4.0),
              child: Text('Login'),
            ),
            TextField(
              onChanged: (value) {
                email = value;
              },
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'your email',
              ),
            ),
            TextButton(
              onPressed: (() => sendEmailLink(email)),
              child: const Text('Send Email Link'),
            ),
          ],
        ),
      ),
    );
  }
}
