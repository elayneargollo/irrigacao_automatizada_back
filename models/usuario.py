from flask import request, url_for, request, url_for
from sql_alchemy import banco
from requests import post
import logging
from config import *

logger = logging.getLogger()

FROM_TITLE = 'API Support Login'
FROM_EMAIL = 'no-replay@restapi.com'

class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'

    usuarioId = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(150), nullable=False)
    sobrenome = banco.Column(banco.String(150), nullable=False)
    email = banco.Column(banco.String(150), nullable=False, unique=True)
    password = banco.Column(banco.String(150), nullable=False)
    ativado = banco.Column(banco.Boolean, default=False)
   
    def __init__(self, nome, sobrenome, email, password, ativado):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.password = password
        self.ativado = ativado

    def json(self):
        return {
            'usuarioId': self.usuarioId,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'ativado': self.ativado
        }

    def send_confirmation_email(self):
        logger.info("Acess send_confirmation_email with email: '{}' in UsuarioModel".format(self.email))

        link =  request.url_root[:-1] + url_for('usuarioconfirmado', usuarioId=self.usuarioId)       

        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api',MAILGUN_API_KEY),
                    data = {'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                           'to': self.email,
                           'subject': 'Confirmação de Cadastro',
                           'text': 'Confirme seu cadastrado clicando no link a seguir: {}'.format(link),
                           'html': '<html><p>\
                               Confirme seu cadastrado clicando no link a seguir: <a href="{}">CONFIRMAR EMAIL</a>\
                                </p></html>'.format(link)
                            }
                    )     

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_usuario(self):
        banco.session.delete(self)
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