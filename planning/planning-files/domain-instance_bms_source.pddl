(define (domain iot-domain-bms_source)

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
		 	(increase (avg_lik) 0.7172391925783972)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6299749640069923)
		 	(increase (avg_len) 1.8995557749259624)
        (increase (num_paths) 4051.0)
		 	(increase (avg_latency) 0.486501307297228)
		 	(mitigation-applied bms_source)
		 )
	 )

(:action strategy-21
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7172391925783972)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6299749640069923)
		 	(increase (avg_len) 1.8995557749259624)
        (increase (num_paths) 4051.0)
		 	(increase (avg_latency) 0.502901493793632)
		 	(mitigation-applied bms_source)
		 )
	 )

(:action strategy-22
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7172391925783972)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6299749640069923)
		 	(increase (avg_len) 1.8995557749259624)
        (increase (num_paths) 4051.0)
		 	(increase (avg_latency) 0.512290785890386)
		 	(mitigation-applied bms_source)
		 )
	 )

(:action strategy-24
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7172391925783972)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6299749640069923)
		 	(increase (avg_len) 1.8995557749259624)
        (increase (num_paths) 4051.0)
		 	(increase (avg_latency) 0.51810931891743)
		 	(mitigation-applied bms_source)
		 )
	 )



)