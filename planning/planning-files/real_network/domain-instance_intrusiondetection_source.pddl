(define (domain iot-domain-intrusiondetection_source)

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
		 	(increase (avg_lik) 0.7098855777952799)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6336443862163033)
		 	(increase (avg_len) 1.935067007019783)
        (increase (num_paths) 6267.0)
		 	(increase (avg_latency) 0.486501307297228)
		 	(mitigation-applied intrusiondetection_source)
		 )
	 )

(:action strategy-21
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7098855777952799)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6336443862163033)
		 	(increase (avg_len) 1.935067007019783)
        (increase (num_paths) 6267.0)
		 	(increase (avg_latency) 0.502901493793632)
		 	(mitigation-applied intrusiondetection_source)
		 )
	 )

(:action strategy-22
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7098855777952799)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6336443862163033)
		 	(increase (avg_len) 1.935067007019783)
        (increase (num_paths) 6267.0)
		 	(increase (avg_latency) 0.512290785890386)
		 	(mitigation-applied intrusiondetection_source)
		 )
	 )

(:action strategy-24
		:parameters (?d -device)
		:precondition (and
		(not (mitigation-applied ?d))
		)
		
		 :effect (and
		 	(increase (avg_lik) 0.7098855777952799)
		 	(increase (avg_imp) %avg_imp%)
		 	(increase (avg_risk) 0.6336443862163033)
		 	(increase (avg_len) 1.935067007019783)
        (increase (num_paths) 6267.0)
		 	(increase (avg_latency) 0.51810931891743)
		 	(mitigation-applied intrusiondetection_source)
		 )
	 )

(:action strategy-14
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
		 	(increase (avg_latency) 0.502168485292079)
		 	(mitigation-applied intrusiondetection_source)
		 )
	 )



)