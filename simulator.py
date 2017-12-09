import process
import time

p1 = process.process()
p1.set_num_process(0)
p1.set_type_client("producer")
p2 = process.process()
p2.set_num_process(1)
p2.set_type_client("consumer")
p3 = process.process()
p2.set_type_client("producer")
p3.set_num_process(2)

p1.init_thread()
p2.init_thread()
p3.init_thread()

time.sleep(2)

p1.begin_requests()
p2.begin_requests()
p3.begin_requests()
