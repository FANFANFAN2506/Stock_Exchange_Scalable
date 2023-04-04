#!/usr/bin/env python3
from utils import printAccountPosition, printOrderStatus
from sqlalchemy import create_engine
engine = create_engine(
    'postgresql://postgres:passw0rd@localhost:5432/hw4_568')

printAccountPosition(engine)
printOrderStatus(engine)
