import random, time, threading


def Aviation():
    global cashout
    x = random.randint(1,20)
    end_counter = x * random.randint(2 , 5)
    counter = 1
    cashout = False
    print(x, end_counter)

    print("🚀 Taking off!")


    while x < end_counter:
        if cashout:
            print(f"Cashout at {round(counter, 3)}!")
            return

        counter = counter + 0.3
        x = x + 0.1
        time.sleep(0.02)



    return {f"Crashed at {round(counter, 3)}!"}


def manual_cashout():
    global cashout
    input("Press ENTER to cash out...")
    cashout = True


aviation_thread = threading.Thread(target=Aviation)
cashout_thread = threading.Thread(target=manual_cashout)

aviation_thread.start()
cashout_thread.start()

aviation_thread.join()
cashout_thread.join()