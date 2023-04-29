import 'dart:async';
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:autocodr/models/user.dart';

class AuthController {
  final String baseUrl =
      "http://127.0.0.1:8000/api"; // 'https://autocodr.com/api'
  final storage = const FlutterSecureStorage();
  User? user;

  final _authStateController = StreamController<bool>.broadcast();
  Stream<bool> get authStateChanges => _authStateController.stream;

  // Singleton
  static final AuthController _singleton = AuthController._internal();

  factory AuthController() => _singleton;

  AuthController._internal();

  bool get isAuthenticated => user != null;

  Future<bool> requestEmailLink(String email) async {
    print("Sending email link to $email");
    try {
      final Map<String, String> headers = {
        'accept': 'application/json',
      };

      final response = await http.post(
        Uri.parse('$baseUrl/request-login?email=$email'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return true;
      } else {
        throw Exception('Failed to request email link');
      }
    } catch (e) {
      print(e.toString());
      return false;
    }
  }

  Future<User?> login(String token) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/login?token=$token'),
      );
      if (response.statusCode == 200) {
        await storage.write(key: 'user', value: response.body);
        user = User.fromJson(jsonDecode(response.body));
        _authStateController.add(true);
        return user;
      } else {
        throw Exception('Failed to log in');
      }
    } catch (e) {
      print(e.toString());
      return null;
    }
  }

  Future<bool> verifyLogin() async {
    final user = this.user;
    if (user != null) {
      try {
        final response = await http.get(
          Uri.parse('$baseUrl/verify-login'),
          headers: <String, String>{
          'Authorization': 'Bearer ${user.accessToken}',
          'accept': 'application/json',
          'Content-Type': 'application/json',
        });

        if (response.statusCode == 200) {
          return true;
        } else {
          String email =
              jsonDecode((await storage.read(key: 'user'))!)['email'];
          await requestEmailLink(email);
          logout();
          return false;
        }
      } catch (e) {
        print(e.toString());
        return false;
      }
    } else {
      return false;
    }
  }

  Future<void> logout() async {
    user = null;
    _authStateController.add(false);
    await storage.delete(key: 'user');
  }
}
