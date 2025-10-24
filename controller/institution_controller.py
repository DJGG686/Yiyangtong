# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 16:04
# @filename: institution_controller
# @function: 
# @version : V1
from flask import Blueprint, Response
from service.institution_service import InstitutionService


class InstitutionController:
    PREFIX = 'institution'

    def __init__(self):
        self.institution_service = InstitutionService()
        self.blueprint = Blueprint('institution_api', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('/list', view_func=self.get_institution_list, methods=['GET'])
        self.blueprint.add_url_rule('/service', view_func=self.get_institution_sercive, methods=['GET'])
        self.blueprint.add_url_rule('/service/order', view_func=self.add_institution_sercive_order, methods=['POST'])
        self.blueprint.add_url_rule('/bed', view_func=self.get_institution_bed, methods=['GET'])
        self.blueprint.add_url_rule('/bed/order', view_func=self.add_institution_sercive_bed, methods=['POST'])

    def get_institution_list(self):
        return Response('institution list', 200)

    def get_institution_sercive(self):
        return Response('institution service', 200)

    def add_institution_sercive_order(self):
        return Response('add institution service order', 200)

    def get_institution_bed(self):
        return Response('institution bed', 200)

    def add_institution_sercive_bed(self):
        return Response('add institution bed order', 200)
