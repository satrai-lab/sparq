(define (problem iot-problem) (:domain iot-domain-app_app36)


;; here we define objects (think of them like variables) that can belong to the "types" defined in the domain file
(:objects 
	app_app36 -device)

(:init
	(not (mitigation-applied app_app36))
	(= (avg_lik) 0)
	(= (avg_imp) 0)
	(= (avg_risk) 0)
	(= (avg_len) 0)
	(= (num_paths) 0)
	(= (avg_latency) 0)

	(= (avg_latency) 0)



)

(:goal (and
	(mitigation-applied app_app36))
)

(:metric minimize  (+ (+ (+ (+
        (* 1 (avg_lik))
        (* 1 (num_paths)))
        (* 1 (avg_risk)))
        (* 1 (avg_len)))
        (* 1 (avg_latency))
))
)

