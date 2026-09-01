import inspect


def test_worker_entrypoint_exists():
    import worker

    assert hasattr(worker, "main")
    assert callable(worker.main)


def test_main_does_not_start_worker_in_lifespan():
    import main

    source = inspect.getsource(main)
    assert "create_task(executar_worker" not in source
