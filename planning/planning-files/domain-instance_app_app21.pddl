(define (domain iot-domain-app_app21)

	(:requirements :strips :typing :conditional-effects :fluents)

	(:types device -object)

	(:predicates
		(mitigation-applied ?d -device)
		(done)
	)

	(:functions

		; security metrics
		(avg_lik)
		(avg_imp)
		(avg_risk)
		(avg_len)
		(num_paths)

		; qos metrics
		(avg_latency)
	)

	
(:action strategy-18
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.764960850862374)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6635314933563835)
		 	(increase (avg_len) 1.8498154981549813)
        (increase (num_paths) 2709.0)
		 	(increase (avg_latency) 0.4947170034137783)
		 	(mitigation-applied app_app21)
		 )
	 )

(:action strategy-19
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.764960850862374)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6635314933563835)
		 	(increase (avg_len) 1.8498154981549813)
        (increase (num_paths) 2709.0)
		 	(increase (avg_latency) 0.487089191322269)
		 	(mitigation-applied app_app21)
		 )
	 )

(:action strategy-2
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7178792919718653)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6312958595721183)
		 	(increase (avg_len) 1.880009657170449)
        (increase (num_paths) 4141.0)
		 	(increase (avg_latency) 0.4969069344027725)
		 	(mitigation-applied app_app21)
		 )
	 )

(:action strategy-9
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7178792919718653)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6312958595721183)
		 	(increase (avg_len) 1.880009657170449)
        (increase (num_paths) 4141.0)
		 	(increase (avg_latency) 0.49776291057398)
		 	(mitigation-applied app_app21)
		 )
	 )



)