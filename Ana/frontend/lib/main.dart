import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const MyApp());
}

const String baseUrl = "http://localhost:8010";

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  Future<void> login() async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": emailController.text,
        "password": passwordController.text,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("token", data["access_token"]);

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const CoursesPage()),
      );
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text("Erro no login")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SizedBox(
          width: 300,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextField(controller: emailController, decoration: const InputDecoration(labelText: "Email")),
              TextField(controller: passwordController, decoration: const InputDecoration(labelText: "Senha"), obscureText: true),
              const SizedBox(height: 20),
              ElevatedButton(onPressed: login, child: const Text("Login")),
            ],
          ),
        ),
      ),
    );
  }
}

class CoursesPage extends StatefulWidget {
  const CoursesPage({super.key});
  @override
  State<CoursesPage> createState() => _CoursesPageState();
}

class _CoursesPageState extends State<CoursesPage> {
  List courses = [];
  final titleController = TextEditingController();
  final descController = TextEditingController();

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString("token");
  }

  Future<void> fetchCourses() async {
    final token = await getToken();
    final response = await http.get(
      Uri.parse("$baseUrl/courses"),
      headers: {"Authorization": "Bearer $token"},
    );

    if (response.statusCode == 200) {
      setState(() {
        courses = jsonDecode(response.body);
      });
    }
  }

  Future<void> createCourse() async {
    final token = await getToken();
    await http.post(
      Uri.parse("$baseUrl/courses"),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token"
      },
      body: jsonEncode({
        "title": titleController.text,
        "description": descController.text
      }),
    );

    titleController.clear();
    descController.clear();
    fetchCourses();
  }

  @override
  void initState() {
    super.initState();
    fetchCourses();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Cursos")),
      body: Column(
        children: [
          Row(
            children: [
              Expanded(child: TextField(controller: titleController, decoration: const InputDecoration(labelText: "Título"))),
              Expanded(child: TextField(controller: descController, decoration: const InputDecoration(labelText: "Descrição"))),
              IconButton(onPressed: createCourse, icon: const Icon(Icons.add)),
            ],
          ),
          Expanded(
            child: ListView.builder(
              itemCount: courses.length,
              itemBuilder: (_, index) {
                return ListTile(
                  title: Text(courses[index]["title"]),
                  subtitle: Text(courses[index]["description"] ?? ""),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
