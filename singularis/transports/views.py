from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


class Transports:

    def __init__(self, *args, **kwargs):
        ...

    def walking(self):
        logger.info(f"walking")


    def bus(self):
        logger.info(f"autobus")

    def train(self):
        logger.info(f"train")

    def airplane(self):
        logger.info(f"fly")