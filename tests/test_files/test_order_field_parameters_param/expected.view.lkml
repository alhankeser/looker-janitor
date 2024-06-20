view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  filter: a_filter_name {
    label: "a filter name"
    hidden: no
    type: number
  }

  dimension: a_dimension_name {
    sql: ${TABLE}."a_dimension_name" ;;
    type: number
    hidden: no
  }

  dimension: b_dimension_name {
    type: number
  }

  measure: a_measure_name {
    filters: [b_dimension_name: "> 10"]
    sql: 
      case when ${a_dimension_name} > 100 then "yes"
        else "no"
      end ;;
    description: "a measure description"
    type: number
  }
}
