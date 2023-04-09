import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const AutoCodr());
}

class AutoCodr extends StatelessWidget {
  const AutoCodr({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const HomePage();
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  HomePageState createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  bool _useAccessToken = false;
  bool isDarkMode() {
    final darkMode = WidgetsBinding.instance.window.platformBrightness;
    if (darkMode == Brightness.dark) {
      return true;
    } else {
      return false;
    }
  }

  Future<int> sendRequest() async {
    var debugUrl = Uri.parse('http://127.0.0.1/api/create_issue');
    var response = await http.post(debugUrl,
        headers: {"auth": "token"}, body: {"issue_url": "_issueUrl"});
    return response.statusCode;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.light().copyWith(
        colorScheme: ThemeData.light().colorScheme.copyWith(
              primary: Colors.deepPurpleAccent,
            ),
      ),
      darkTheme: ThemeData.dark().copyWith(
        colorScheme: ThemeData.dark().colorScheme.copyWith(
              primary: Colors.deepPurpleAccent,
            ),
      ),
      themeMode: isDarkMode() ? ThemeMode.dark : ThemeMode.light,
      home: Scaffold(
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
                child: const TextField(
                  decoration: InputDecoration(
                    labelText: 'github issue link',
                    border: OutlineInputBorder(),
                  ),
                ),
              ),
              if (_useAccessToken)
                Container(
                  constraints: const BoxConstraints(maxWidth: 420),
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: const TextField(
                    decoration: InputDecoration(
                      labelText: 'access token',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {},
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
      ),
    );
  }
}
