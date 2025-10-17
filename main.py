import verification
import verification_promise

for k in 2,3,4,5:

    # Verification of tables corresponding to tractability and hardness of fiPCSP(A, OR)
    print('Verifying coverage', flush=True)
    result_coverage = verification.verify_coverage(k)
    print('Verifying tractability', flush=True)
    result_tractability = verification.verify_tractability(k)
    print('Verifying hardness', flush=True)
    result_hardness = verification.verify_hardness(k)
    print('Verifying block symmetries', flush=True)
    result_block_sym = verification.verify_block_sym(k)
    print('Verifying that representatives used is lexographically the smallest possible', flush=True)
    result_representative_lexographically_smallest = verification.verify_representative_lexographically_smallest(k)
    print('Verifying counts of tractable/unknown/hard representatives', flush=True)
    result_counts = verification.verify_counts(k)

    # Verification of tables correponding to promise-useful/uselessness
    print('Verifying coverage for promise', flush=True)
    result_promise_coverage = verification_promise.verify_coverage(k)
    print('Verifying usefulness for promise', flush=True)
    result_promise_usefulness = verification_promise.verify_promise_usefulness(k)
    print('Verifying uselessness for promise', flush=True)
    result_promise_uselessness = verification_promise.verify_promise_uselessness(k)
    print('Verifying that representatives used for promise is lexiographically the smallest possible', flush=True)
    result_promise_representative_lexographically_smallest = verification_promise.verify_representative_lexographically_smallest(k)
    print('Verifying counts of promise-useful/unknown/useless representatives', flush=True)
    result_promise_counts = verification_promise.verify_counts(k)

    print('-----------------------------------------------------------------------')
    print()
    print('Summary of results for k = %d:' % k)
    print('Verification of coverage:', ['FAILED', 'SUCCESS'][result_coverage])
    print('Verification of tractability:', ['FAILED', 'SUCCESS'][result_tractability])
    print('Verification of hardness:', ['FAILED', 'SUCCESS'][result_hardness])
    print('Verification of block symmetry:', ['FAILED', 'SUCCESS'][result_block_sym])
    print('Verification of lexographically smallest possible representatives:', ['FAILED', 'SUCCESS'][result_representative_lexographically_smallest])
    print('Verification of counts of tractable/unknown/hard representatives:', ['FAILED', 'SUCCESS'][result_counts])
    
    print('Verification of coverage for promise:', ['FAILED', 'SUCCESS'][result_promise_coverage])
    print('Verification of promise usefulness:', ['FAILED', 'SUCCESS'][result_promise_usefulness])
    print('Verification of promise uselessness:', ['FAILED', 'SUCCESS'][result_promise_uselessness])
    print('Verification of lexographically smallest possible representatives for promise:', ['FAILED', 'SUCCESS'][result_promise_representative_lexographically_smallest])
    print('Verification of counts of promise-useful/unknown/useless representatives:', ['FAILED', 'SUCCESS'][result_promise_counts])
    print()
    print('-----------------------------------------------------------------------')


    if k == 4:
        print('WARNING: Next verification is k = 5. This is both slow and requires a significant amount of RAM. Using PyPy is recommended.')
    input('Press enter to continue')

