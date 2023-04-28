import 'package:autocodr/controller/auth.dart';
import 'package:autocodr/pages/login.dart';
import 'package:flutter/material.dart';
import 'pages/home.dart';

class AutoCodr extends StatelessWidget {
  AutoCodr({Key? key}) : super(key: key);

  final authController = AuthController();

  bool get isDarkMode {
    return WidgetsBinding.instance.window.platformBrightness == Brightness.dark;
  }

  ThemeData get lightTheme {
    return ThemeData.light().copyWith(
      colorScheme: ThemeData.light().colorScheme.copyWith(
            primary: Colors.deepPurpleAccent,
          ),
    );
  }

  ThemeData get darkTheme {
    return ThemeData.dark().copyWith(
      colorScheme: ThemeData.dark().colorScheme.copyWith(
            primary: Colors.deepPurpleAccent,
          ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '🤖AutoCodr',
      theme: lightTheme,
      darkTheme: darkTheme,
      themeMode: isDarkMode ? ThemeMode.dark : ThemeMode.light,
      initialRoute: '/',
      routes: {
        '/': (context) => const HomePage(),
        '/login': (context) => const LoginScreen(),
      },
    );
  }

}
