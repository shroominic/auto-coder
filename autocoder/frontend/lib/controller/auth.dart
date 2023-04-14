import 'package:autocodr/models/user.dart';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AuthController {
  final String baseUrl = "http://127.0.0.1/api"; // 'https://autocodr.com/api'
  final storage = const FlutterSecureStorage();
  User? user;

  Future<bool> requestEmailLink(String email) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/request-login'),
        body: {'email': email},
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
        return User.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Failed to log in');
      }
    } catch (e) {
      print(e.toString());
      return null;
    }
  }

  Future<bool> isAuthenticated() async {
    if (user != null) {
      return true;
    } else {
      String? jsonUser = await storage.read(key: 'user');
      if (jsonUser == null) {
        return false;
      } else {
        user = User.fromJson(jsonDecode(jsonUser));
        return true;
      }
    }
  }

  Future<bool> verifyLogin() async {
    if (await isAuthenticated()) {
      try {
        final response = await http.get(
          Uri.parse('$baseUrl/verify-login'),
        );

        if (response.statusCode == 200) {
          return true;
        } else {
          String email =
              jsonDecode((await storage.read(key: 'user'))!)['email'];
          await requestEmailLink(email);
          storage.delete(key: 'user');
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
    await storage.delete(key: 'user');
  }
}
