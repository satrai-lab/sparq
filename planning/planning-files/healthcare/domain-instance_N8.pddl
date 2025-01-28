(define (domain iot-domain-N8)

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
		 	(increase (avg_lik) 0.428263289279012)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.0228022318956793)
		 	(increase (avg_len) 1.903254972875226)
        (increase (num_paths) 1105.0)
		 	(increase (avg_latency) 0.486501307297228)
		 	(mitigation-applied N8)
		 )
	 )

(:action strategy-21
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.428263289279012)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.0228022318956793)
		 	(increase (avg_len) 1.903254972875226)
        (increase (num_paths) 1105.0)
		 	(increase (avg_latency) 0.502901493793632)
		 	(mitigation-applied N8)
		 )
	 )

(:action strategy-22
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.428263289279012)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.0228022318956793)
		 	(increase (avg_len) 1.903254972875226)
        (increase (num_paths) 1105.0)
		 	(increase (avg_latency) 0.512290785890386)
		 	(mitigation-applied N8)
		 )
	 )

(:action strategy-24
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.428263289279012)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.0228022318956793)
		 	(increase (avg_len) 1.903254972875226)
        (increase (num_paths) 1105.0)
		 	(increase (avg_latency) 0.51810931891743)
		 	(mitigation-applied N8)
		 )
	 )



)