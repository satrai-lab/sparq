(define (domain iot-domain-amazonecho_source)

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

	
(:action strategy-20
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7272435741355476)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6441025159801559)
		 	(increase (avg_len) 1.849621785173979)
        (increase (num_paths) 3304.0)
		 	(increase (avg_latency) 0.486501307297228)
		 	(mitigation-applied amazonecho_source)
		 )
	 )

(:action strategy-21
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7272435741355476)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6441025159801559)
		 	(increase (avg_len) 1.849621785173979)
        (increase (num_paths) 3304.0)
		 	(increase (avg_latency) 0.502901493793632)
		 	(mitigation-applied amazonecho_source)
		 )
	 )

(:action strategy-22
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7272435741355476)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6441025159801559)
		 	(increase (avg_len) 1.849621785173979)
        (increase (num_paths) 3304.0)
		 	(increase (avg_latency) 0.512290785890386)
		 	(mitigation-applied amazonecho_source)
		 )
	 )

(:action strategy-24
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7272435741355476)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6441025159801559)
		 	(increase (avg_len) 1.849621785173979)
        (increase (num_paths) 3304.0)
		 	(increase (avg_latency) 0.51810931891743)
		 	(mitigation-applied amazonecho_source)
		 )
	 )



)