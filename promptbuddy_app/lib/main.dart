import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const PromptBuddyApp());
}

class PromptBuddyApp extends StatelessWidget {
  const PromptBuddyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PromptBuddy Translator',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const TranslatorPage(),
    );
  }
}

class TranslatorPage extends StatefulWidget {
  const TranslatorPage({super.key});

  @override
  State<TranslatorPage> createState() => _TranslatorPageState();
}

class _TranslatorPageState extends State<TranslatorPage> {
  final TextEditingController _controller = TextEditingController();

  String _selectedSourceLang = "english"; // default source
  String _selectedTargetLang = "hindi";   // default target
  String _result = "";
  bool _isLoading = false;

  final List<String> _languages = [
    "english",
    "hindi",
    "marathi",
    "tamil",
    "telugu",
    "kannada",
    "bengali",
    "punjabi",
    "gujarati",
    "malayalam",
    "odia",
    "assamese",
    "urdu",
  ];

  Future<void> _translateText() async {
    if (_controller.text.isEmpty) return;

    setState(() {
      _isLoading = true;
      _result = "";
    });

    try {
      final response = await http.post(
        Uri.parse("http://10.18.31.71:8000/translate"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "text": _controller.text,
          "src_lang": _selectedSourceLang,
          "tgt_lang": _selectedTargetLang,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _result = data["translation"] ?? "No result";
        });
      } else {
        setState(() {
          _result = "Error: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        _result = "Failed to connect to backend";
      });
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("PromptBuddy Translator")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: "Enter text",
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),

            // Source Language Dropdown
            DropdownButtonFormField(
              value: _selectedSourceLang,
              decoration: const InputDecoration(
                labelText: "Source Language",
                border: OutlineInputBorder(),
              ),
              items: _languages
                  .map((lang) => DropdownMenuItem(
                        value: lang,
                        child: Text(lang[0].toUpperCase() + lang.substring(1)),
                      ))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  _selectedSourceLang = value.toString();
                });
              },
            ),
            const SizedBox(height: 12),

            // Target Language Dropdown
            DropdownButtonFormField(
              value: _selectedTargetLang,
              decoration: const InputDecoration(
                labelText: "Target Language",
                border: OutlineInputBorder(),
              ),
              items: _languages
                  .map((lang) => DropdownMenuItem(
                        value: lang,
                        child: Text(lang[0].toUpperCase() + lang.substring(1)),
                      ))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  _selectedTargetLang = value.toString();
                });
              },
            ),
            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: _isLoading ? null : _translateText,
              child: _isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Translate"),
            ),
            const SizedBox(height: 20),

            Text(
              _result,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }
}
