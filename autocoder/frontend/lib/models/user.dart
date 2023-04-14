class User {
  final String email;
  final String accessToken;

  User({required this.email, required this.accessToken});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      email: json['email'],
      accessToken: json['access_token'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'access_token': accessToken,
    };
  }
}
