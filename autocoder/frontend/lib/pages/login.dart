import 'package:autocodr/controller/auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  @override
  String email = '';
  final authController = AuthController();

  void sendEmailLink(String email) async {
    if (email.contains('@')) {
      await authController.requestEmailLink(email);
    }
  }

  Widget build(BuildContext context) {
    return Column(
      children: [
        const Text('Login'),
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
    );
  }
}

class LoginButton extends StatelessWidget {
  LoginButton({super.key, required this.showLoginScreen});

  bool showLoginScreen;

  loginButton() {
    showLoginScreen = !showLoginScreen;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: TextButton(
        onPressed: loginButton,
        child: const Text('Login'),
      ),
    );
  }
}
