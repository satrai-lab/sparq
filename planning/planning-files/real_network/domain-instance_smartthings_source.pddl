(define (domain iot-domain-smartthings_source)

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
		 	(increase (avg_lik) 0.793615272272811)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6219654558145659)
		 	(increase (avg_len) 1.8655097613882865)
        (increase (num_paths) 460.0)
		 	(increase (avg_latency) 0.486501307297228)
		 	(mitigation-applied smartthings_source)
		 )
	 )

(:action strategy-21
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.793615272272811)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6219654558145659)
		 	(increase (avg_len) 1.8655097613882865)
        (increase (num_paths) 460.0)
		 	(increase (avg_latency) 0.502901493793632)
		 	(mitigation-applied smartthings_source)
		 )
	 )

(:action strategy-22
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.793615272272811)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6219654558145659)
		 	(increase (avg_len) 1.8655097613882865)
        (increase (num_paths) 460.0)
		 	(increase (avg_latency) 0.512290785890386)
		 	(mitigation-applied smartthings_source)
		 )
	 )

(:action strategy-24
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.793615272272811)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6219654558145659)
		 	(increase (avg_len) 1.8655097613882865)
        (increase (num_paths) 460.0)
		 	(increase (avg_latency) 0.51810931891743)
		 	(mitigation-applied smartthings_source)
		 )
	 )

(:action strategy-14
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7203863058792638)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6330555244001074)
		 	(increase (avg_len) 1.8814344962185896)
        (increase (num_paths) 4098.0)
		 	(increase (avg_latency) 0.502168485292079)
		 	(mitigation-applied smartthings_source)
		 )
	 )



)