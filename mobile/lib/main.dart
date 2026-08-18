import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'screens/landing_screen.dart';
import 'screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  final String? token = prefs.getString('token');
  
  runApp(PelitaGuardApp(startWithHome: token != null));
}

class PelitaGuardApp extends StatelessWidget {
  final bool startWithHome;
  
  const PelitaGuardApp({super.key, required this.startWithHome});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PelitaGuard',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
      ),
      home: startWithHome ? const HomeScreen() : const LandingScreen(),
    );
  }
}
