from sql_alchemy import banco

class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'

    usuarioId = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(150), nullable=False)
    sobrenome = banco.Column(banco.String(150), nullable=False)
    email = banco.Column(banco.String(150), nullable=False)
    password = banco.Column(banco.String(150), nullable=False)
   
    def __init__(self, nome, sobrenome, email, password):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.password = password

    def json(self):
        return {
            'usuarioId': self.usuarioId,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email
        }

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    @classmethod
    def find_usuario(cls, usuarioId):
        usuario = cls.query.filter_by(usuarioId=usuarioId).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def find_by_email(cls, email):
        usuario = cls.query.filter_by(email=email).first()
        if usuario:
            return usuario
        return None