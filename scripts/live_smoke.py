# Purpose: Guard the unwired paid prelabel transport.
import os
if not os.getenv('TYPESAFE_API_KEY'):raise SystemExit('Set TYPESAFE_API_KEY')
raise SystemExit('Live prelabel transport is not wired in this alpha; zero requests made')
