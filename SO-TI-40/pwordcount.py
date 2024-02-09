### Grupo: SO-TI-40
### Aluno 1: João Ferreira (fc54600)
### Aluno 2: João Assunção (fc56902)
### Aluno 3: Diogo Piçarra (fc60858)

import sys
import argparse
import multiprocessing
from collections import Counter
import time
from datetime import datetime
from multiprocessing import Value, Array, Manager, Lock
import signal

# Global variables for partial results
total_words_counter = Value('i', 0)
unique_words_counters = None
word_occurrence_counters = None
processed_files_counter = Value('i', 0)
remaining_files_counter = Value('i', 0)

# Locks for synchronization
total_words_lock = Lock()
processed_files_lock = Lock()
remaining_files_lock = Lock()

# Global variable for the multiprocessing pool
pool = None

def print_partial_results(log_file, start_time):
    current_time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    elapsed_time = int((time.time() - start_time) * 1e6)

    with total_words_lock:
        total_words = total_words_counter.value

    with processed_files_lock:
        processed_files = processed_files_counter.value

    with remaining_files_lock:
        remaining_files = remaining_files_counter.value

    if log_file:
        with open(log_file, 'a') as log:
            log.write(f"{current_time} {elapsed_time} {total_words} {processed_files} {remaining_files}\n")
    else:
        print(f"{current_time} {elapsed_time} {total_words} {processed_files} {remaining_files}")

def count_words_in_file(file_path, mode, unique_words_queue=None, word_occurrence_queue=None):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            words = content.split()

            if mode == 't':
                with total_words_lock:
                    total_words_counter.value += len(words)
            elif mode == 'u':
                unique_words = set(words)
                unique_words_queue.put(unique_words)
            elif mode == 'o':
                word_counts = Counter(words)
                word_occurrence_queue.put(word_counts)

    except FileNotFoundError:
        print(f'Arquivo não encontrado: {file_path}')
    except Exception as e:
        print(f'Erro ao processar arquivo {file_path}: {str(e)}')

def process_file(file_path, mode, unique_words_queue=None, word_occurrence_queue=None):
    result = count_words_in_file(file_path, mode, unique_words_queue, word_occurrence_queue)

def main(args):
    global pool  # Make pool a global variable

    parser = argparse.ArgumentParser(description='Calcula palavras em um ou mais ficheiros.')
    parser.add_argument('-m', choices=['t', 'u', 'o'], default='t', help='Modo de contagem (t, u ou o)')
    parser.add_argument('-p', type=int, default=1, help='Nível de paralelização')
    parser.add_argument('-i', type=int, default=3, help='Intervalo de tempo em segundos para resultados parciais')
    parser.add_argument('-l', help='Nome do arquivo de log para resultados parciais')
    parser.add_argument('files', nargs='+', help='Ficheiros para contar palavras')
    args = parser.parse_args()

    mode = args.m
    parallelism_level = args.p
    interval = args.i
    log_file = args.l
    files = args.files

    if parallelism_level > len(files):
        parallelism_level = len(files)

    # Initialize shared data structures
    global unique_words_counters
    global word_occurrence_counters
    unique_words_counters = [Array('i', [0] * parallelism_level) for _ in range(parallelism_level)]
    word_occurrence_counters = [Array('i', [0] * parallelism_level) for _ in range(parallelism_level)]

    manager = Manager()
    unique_words_queue = manager.Queue()
    word_occurrence_queue = manager.Queue()

    pool = multiprocessing.Pool(processes=parallelism_level)

    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)

    start_time = time.time()

    try:
        async_results = []

        for i in range(len(files)):
            async_result = pool.apply_async(process_file, args=(files[i], mode, unique_words_queue, word_occurrence_queue))
            async_results.append(async_result)

        for async_result in async_results:
            async_result.get()  # Wait for each result before updating remaining_files_counter
            with remaining_files_lock:
                remaining_files_counter.value += 1

            time.sleep(interval)
            print_partial_results(log_file, start_time)

    except KeyboardInterrupt:
        print("Processamento interrompido pelo utilizador.")
    finally:
        pool.close()
        pool.join()

        print_partial_results(log_file, start_time)

        # Aggregate results
        if mode == 't':
            print(f'Total de palavras: {total_words_counter.value}')
        elif mode == 'u':
            unique_words = set()
            while not unique_words_queue.empty():
                unique_words.update(unique_words_queue.get())
            print(f'Total de palavras únicas: {len(unique_words)}')
        elif mode == 'o':
            word_counts = Counter()
            while not word_occurrence_queue.empty():
                word_counts.update(word_occurrence_queue.get())

            for word, count in word_counts.items():
                print(f'{word}: {count}')

def signal_handler(signal, frame):
    print("\nRecebido sinal SIGINT (Ctrl+C). Aguardando processos filhos terminarem...")
    pool.terminate()
    pool.join()

if __name__ == "__main__":
    main(sys.argv[1:])