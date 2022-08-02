from Utils import server

# logic-server vk
server.Server().start()

# restart server everyday
server.check_restart()
