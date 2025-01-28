(define (domain iot-domain-app_app11)

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
		 	(increase (avg_lik) 0.6370967840991362)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.5985926514960396)
		 	(increase (avg_len) 1.860041265474553)
        (increase (num_paths) 2907.0)
		 	(increase (avg_latency) 0.4947170034137783)
		 	(mitigation-applied app_app11)
		 )
	 )

(:action strategy-19
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.6370967840991362)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.5985926514960396)
		 	(increase (avg_len) 1.860041265474553)
        (increase (num_paths) 2907.0)
		 	(increase (avg_latency) 0.487089191322269)
		 	(mitigation-applied app_app11)
		 )
	 )

(:action strategy-2
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7152875700262351)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.629265360826807)
		 	(increase (avg_len) 1.8789576229907448)
        (increase (num_paths) 4105.0)
		 	(increase (avg_latency) 0.4969069344027725)
		 	(mitigation-applied app_app11)
		 )
	 )

(:action strategy-9
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7152875700262351)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.629265360826807)
		 	(increase (avg_len) 1.8789576229907448)
        (increase (num_paths) 4105.0)
		 	(increase (avg_latency) 0.49776291057398)
		 	(mitigation-applied app_app11)
		 )
	 )



)