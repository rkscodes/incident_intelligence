{#
This macro returns month names 
#}
{% macro get_month_name(incident_month) %}
case
    {{ incident_month }}
    when 1
    then 'January'
    when 2
    then 'February'
    when 3
    then 'March'
    when 4
    then 'April'
    when 5
    then 'May'
    when 6
    then 'June'
    when 7
    then 'July'
    when 8
    then 'August'
    when 9
    then 'September'
    when 10
    then 'October'
    when 11
    then 'November'
    when 12
    then 'December'
end
{% endmacro %}
