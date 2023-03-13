import asyncio
import shlex
from cowsay import cowsay, list_cows

users = {}
clients = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    users[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(users[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

        names = [i[0] for i in list(clients.values())]

        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                message = shlex.split(q.result().decode().strip())
                match message:
                    case ["login", nickname]:
                        if me in clients:
                            await clients[me].put("You are already logged in.")
                        elif nickname in list_cows():
                            if nickname not in names:
                                clients[me] = [nickname, me]
                                await users[me].put("Successful login.")

                            else:
                                await users[me].put("This nickname is already taken.\nCheck the list of available names with the 'cows' command")

                        else:
                            await users[me].put("This nickname is not supported.\nCheck the list of available names with the 'cows' command")

                    case ["who"]:
                        if me not in clients:
                            await users[me].put("You are not logged in.\nCheck the list of available names with the 'cows' command")
                        else:
                            msg = ''
                            for i in names:
                                msg += i + '\n'
                            await users[me].put(msg)

                    case ["cows"]:
                        res = [cow for cow in list_cows() if cow not in names]
                        msg = ''
                        for i in res:
                            msg += i + '\n'
                        await users[me].put(msg)

                    case ["say", *args]:
                        if me not in clients:
                            await users[me].put("You are not logged in.\nCheck the list of available names with the 'cows' command")
                        else:
                            if len(args) != 2:
                                await users[me].put("Invalid arguments.")
                            else:
                                if args[1] not in names:
                                    await users[me].put("User does not exist.")
                                else:
                                    receiver = None
                                    for i in list(clients.values()):
                                        if i[0] == args[1]:
                                            receiver = i[1]

                                    await users[receiver].put(f"Message from: {clients[me][0]}\nTo: you\n" + cowsay(message=args[0], cow=clients[me][0]))

                    case ["yield", *args]:
                        if me not in clients:
                            await users[me].put("You are not logged in.\nCheck the list of available names with the 'cows' command")
                        else:
                            for i in clients.values():
                                if users[me] != users[i[1]]:
                                    await users[i[1]].put(f"Message from: {clients[me][0]}\nTo: everyone\n" + cowsay(message=args[0], cow=clients[me][0]))

                    case ["quit"]:
                        if me not in clients:
                            await users[me].put("You are not logged in.\nCheck the list of available names with the 'cows' command")
                        else:
                            send.cancel()
                            receive.cancel()

                            del clients[me], users[me]

                            writer.close()

                            await writer.wait_closed()
                            return

                    case _:
                        if me not in clients:
                            await users[me].put("You are not logged in.\nCheck the list of available names with the 'cows' command")
                        else:
                            await users[me].put("Invalid command.")

            elif q is receive:
                receive = asyncio.create_task(users[me].get())
                writer.write(f"{q.result()}\n".encode())

                await writer.drain()

    send.cancel()
    receive.cancel()

    del users[me]
    writer.close()

    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

