# controller tests
if False: 
    from controller import unitTest
    # unitTest.testPromptStack()
    if True:
        def aiAdapterTest():
            unitTest.testAiAdapter("Explain what a gpu is.")
        def aiAdapterTest2():
            unitTest.testAiAdapter("Explain how to make a sandwich.")
        def aiAdapterTest3():
            unitTest.testAiAdapter("Get me a joke about a cat.")
        from threading import Thread
        thread1 = Thread(target=aiAdapterTest)
        thread2 = Thread(target=aiAdapterTest2)
        thread3 = Thread(target=aiAdapterTest3)
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()
