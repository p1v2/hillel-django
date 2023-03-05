# from datetime import datetime
# from threading import Thread


class Sum:
    total = 0


def calculate_sum(start, end):
    for i in range(start, end):
        Sum.total += i


if __name__ == "__main__":
    # start = datetime.now()
    # sum1_thread = Thread(target=calculate_sum, args=(0, 100000000))
    # # sum2_thread = Thread(target=calculate_sum, args=(25000001, 50000000))
    # # sum3_thread = Thread(target=calculate_sum, args=(50000001, 75000000))
    # # sum4_thread = Thread(target=calculate_sum, args=(75000001, 100000000))
    #
    # sum1_thread.start()
    # # sum2_thread.start()
    # # sum3_thread.start()
    # # sum4_thread.start()
    #
    # sum1_thread.join()
    # # sum2_thread.join()
    # # sum3_thread.join()
    # # sum4_thread.join()
    #
    # end = datetime.now()
    #
    # print(Sum.total)
    # print((end - start).total_seconds())
    calculate_sum(0, 100000000)
    print(Sum.total)
